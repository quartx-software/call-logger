# Third Party
import pytest

# Local
from calllogger.plugins.internal import siemens_serial
from calllogger.record import CallDataRecord
from ..common import call_plugin
from calllogger import running


good_lines = b"""
10.04.1923:19:06  2   104     00:00:0500441619251900                       2
10.04.1923:28:01  2      00:0100:00:000061393038625                        2
10.04.1923:28:01  2      00:0100:00:000061393038625                        2
10.04.1923:28:01  2      00:0100:00:000061393038625                        2
10.04.1923:19:06  2   104     00:00:0500441619251900                       2
11.04.1900:33:20  1   104     00:00:020857739075                           9
11.04.1900:34:13  2   104     00:00:060876153281                           2
11.04.1900:35:38  1   104             0876153281                           0
11.04.1900:35:38  1   103             0876153281                           0
11.04.1900:35:48  1   10400:0100:00:070876153281                           1
11.04.1900:36:28  2   104             79923                                0
11.04.1900:36:29  2   103             79923                                0
11.04.1900:36:34  2   10000:0500:00:0079923                                1
11.04.1900:49:13  1   104             0876153281                           0
11.04.1900:49:13  1   103             0876153281                           0
11.04.1900:49:22  2   104     00:00:030857739075                           2
11.04.1900:49:24  1   10000:1000:00:000876153281                           1
09.09.1821:04:01  1   100             0811111111                           009923
09.09.1820:16:50  1   10000:0100:00:060877629926                           1 9923
02.09.1814:07:40  1   10000:0900:00:000877629926                           2
22.02.1923:11:41  3   048             0248873711                           0 4416
22.02.1923:11:43  3   04800:4100:10:030248873711                           154416
22.02.1922:55:27  3   05800:0700:00:000922735086                           2
11.04.1914:58:19  1   103                                                  0
11.12.0008:23:23  4    16     00:05:2302317324856                       12 2                902725  841
11.12.0009:12:45  3    18     00:01:23834756                            34 212345678901                 2
11.12.0009:25:34  2    1100:34                                             1
11.12.0010:01:46  1    12     00:12:5383726639046287127384               5 2
11.12.0010:03:42  2    14     05:42:4338449434444495598376             245 2
11.12.0010:23:24  2    15     00:02:221234567890123412????              83 2
11.12.0011:12:45  3    18     00:01:23834756                            34 2
12.12.0012:23:34  3    1200:1500:03:12                                     1
12.12.0012:23:50  4    11     00:03:583844733399                         7 2
12.12.0013:23:54  3    17     00:02:233844733399                         8 5
12.12.0014:05:24  3    18     00:01:23834756                            31 2
12.12.0014:38:43  2    12     00:03:242374844                           63 2
12.12.0014:43:33  3    12     00:00:255345545556                         5 2
12.12.0014:44:12  2    12     00:12:122374844                           12 8
12.12.0014:44:12  3    12     00:12:125345545556                        10 8
12.12.0014:56:24  2    12     00:23:462374844                           84 2
13.12.0009:43:52  1     5     00:01:0539398989983                       76 4
14.12.0012:23:34  1     600:1400:02:3427348596872347569036                 3
15.12.0009:44:34  4    15     00:02:12189????                           23 2
15.12.0009:56:33  3    14     00:05:451283394495                        28 2
15.12.0012:20:26  1    12             0230298007766                        0
15.12.0012:23:34  1    1200:3400:02:340230298007766                        1
15.12.0013:43:25  3    15     00:05:2408972212345                          1
15.12.0013:43:25  4    15     00:05:24023147115432174                      9
15.12.0013:45:28  4    18             0230298007252                        0
15.12.0013:45:28  4    32             0230298007252                        0
15.12.0013:45:28  4    16             0230298007252                        0
15.12.0013:46:18  4    1600:50        0230298007252                        1
15.12.0013:49:28  4    16     00:00:0002317324856                          2
01.01.0000:00:00  8                                                     23 2
31.01.2115:23:44  9   500             353877629926                         0
31.01.2115:23:49  9   250             353877629926                         0
31.01.2115:23:58  9   25000:0500:00:07353877629926                         1
31.01.2115:24:25  9   110     00:00:26353877629926                        35
31.01.2115:24:35  9   223     00:00:10353877629926                        35
31.01.2115:24:51  9   500             353877629926                         0
31.01.2115:24:57  9   251             353877629926                         0
31.01.2115:25:04  9   25100:0500:00:07353877629926                         1
31.01.2115:25:43  5   110     00:00:130857739075                           2
31.01.2115:26:22  5   110     00:00:080857739075                           2
31.01.2115:26:22  9   110     00:01:17353877629926                        35
31.01.2115:26:38  5   110     00:00:150857739075                          38
31.01.2115:26:39  9   110     00:00:16353877629926                        37
31.01.2115:28:21  9   500             353877629926                         0
31.01.2115:28:27  9   250             353877629926                         0
31.01.2115:28:34  9   25000:0500:00:06353877629926                         1
31.01.2115:29:29  5   110     00:00:300857739075                           2
31.01.2115:29:29  9   110     00:00:55353877629926                        35
31.01.2115:29:42  5   110     00:00:120857739075                          38
31.01.2115:29:42  9   110     00:00:12353877629926                        37
31.01.2115:34:58  5   110     00:00:140857739075                           2
31.01.2115:35:09  5   223     00:00:110857739075                          36
31.01.2115:37:45  9   500             353877629926                         0
31.01.2115:37:50  9   251             353877629926                         0
31.01.2115:37:58  9   25100:0500:00:07353877629926                         1
31.01.2115:38:17  9   110     00:00:18353877629926                        35
31.01.2115:38:20  9   117     00:00:03353877629926                        35
31.01.2115:39:41 16   11000:0800:00:0002976570                             2
31.01.2115:40:53  5   110     00:00:320877629926                           2
31.01.2115:41:52  5   110     00:00:190877629926                           2
31.01.2115:41:57  5   117     00:00:050877629926                          36
31.01.2115:50:41  5   500                                                  0
31.01.2115:50:47  5   250                                                  0
31.01.2115:50:58  5   25000:0500:00:10                                     1
31.01.2115:51:04  5   110     00:00:06                                    35
31.01.2116:04:14  9   500             353877629926                         0
31.01.2116:04:15  9   50000:0100:00:00353877629926                         1
31.01.2116:04:30  9   500             353877629926                         0
31.01.2116:04:35  9   250             353877629926                         0
31.01.2116:04:52  9   25000:0500:00:16353877629926                         1
31.01.2116:04:56  9   117     00:00:04353877629926                        35
31.01.2116:06:20  9   500             353877629926                         0
31.01.2116:06:25  9   251             353877629926                         0
31.01.2116:06:43  5   110     00:00:010857739075                           9
31.01.2116:06:43  9   25100:0500:00:16353877629926                         1
31.01.2116:06:59  5   110     00:00:160857739075                          39
31.01.2116:06:59  9   251     00:00:16353877629926                        37
31.01.2116:08:16  9   500             353877629926                         0
31.01.2116:08:21  9   250             353877629926                         0
31.01.2116:08:39  6   110     00:00:010857739085                           9
31.01.2116:08:39  9   25000:0500:00:16353877629926                         1
31.01.2116:08:41  6   110     00:00:020857739085                          39
31.01.2116:08:41  9   250     00:00:02353877629926                        37
31.01.2116:09:07  9   500             353877629926                         0
31.01.2116:09:13  9   251             353877629926                         0
31.01.2116:09:30  6   110     00:00:010857739075                           9
31.01.2116:09:30  9   25100:0500:00:16353877629926                         1
31.01.2116:09:47  6   110     00:00:170857739075                          39
31.01.2116:09:48  9   251     00:00:17353877629926                        37
31.01.2116:22:13  9   500             353877629926                         0
31.01.2116:22:14  9   50000:0100:00:00353877629926                         1
31.01.2116:22:34  9   500             353877629926                         0
31.01.2116:22:39  9   250             353877629926                         0
31.01.2116:22:56  5   110     00:00:010857739075                           9
31.01.2116:22:56  9   25000:0500:00:16353877629926                         1
31.01.2116:23:12  5   110     00:00:150857739075                          39
31.01.2116:23:12  9   250     00:00:15353877629926                        37
31.01.2116:25:18  9   500             353877629926                         0
31.01.2116:25:23  9   251             353877629926                         0
31.01.2116:25:30  9   25100:0500:00:05353877629926                         1
31.01.2116:25:56  5   110     00:00:090857739075                           2
31.01.2116:26:37  5   110     00:00:080857739075                           2
31.01.2116:26:37  9   110     00:01:07353877629926                        35
31.01.2116:26:39  5   110     00:00:020857739075                          38
31.01.2116:26:39  9   110     00:00:02353877629926                        37
31.01.2115:23:44  9   500             353877629926                         0
31.01.2115:23:49  9   250             353877629926                         0
31.01.2115:23:58  9   25000:0500:00:07353877629926                         1
31.01.2115:24:25  9   110     00:00:00353877629926                        35
\x10\x02\x10\x03\x13\x1123.05.2105:25:49  1   100             0869182940                           0
\x10\x02\x10\x03\x13\x1127.04.2121:33:56  3   100             0876940494                           0
\x10\x02\x10\x03\x13\x1130.03.2121:12:21  3   100             0860610095                           0
""".strip().split(b"\n")


@pytest.fixture(autouse=True)
def mock_port(mock_serial_port):
    return mock_serial_port


@pytest.fixture
def mock_plugin(mocker):
    plugin = call_plugin(siemens_serial.SiemensHipathSerial)
    mocked_runner = mocker.patch.object(running, "is_set")
    mocked_runner.side_effect = [True, False]
    # This will protect from slow failing tests
    mocker.patch.object(plugin.timeout, "sleep")
    yield plugin


@pytest.mark.parametrize("raw_line", good_lines)
def test_parser_good_lines(mock_plugin: siemens_serial.SiemensHipathSerial, raw_line):
    """Test that the serial parser parses all known line formats."""
    decoded_line = mock_plugin.decode(raw_line)
    assert isinstance(decoded_line, str)

    validated_line = mock_plugin.validate(decoded_line)
    assert isinstance(decoded_line, str)

    record = mock_plugin.parse(validated_line)
    assert isinstance(record, CallDataRecord)
    assert isinstance(record.call_type, int)


@pytest.mark.parametrize("raw_line", [
    b"dfdfdfsdfxcvnbdfsdfasdfa",  # Totally invalid line
    b"31.01.2116:23:12  9   250     00:00:1535387",  # Line is missing data, too short
])
def test_validate_bad_lines(mock_plugin: siemens_serial.SiemensHipathSerial, raw_line):
    """Test that the serial parser parses all known line formats."""
    decoded_line = mock_plugin.decode(raw_line)
    assert isinstance(decoded_line, str)

    validated_line = mock_plugin.validate(decoded_line)
    assert validated_line is False


@pytest.mark.parametrize("raw_line", good_lines)
def test_full_serial_parser_good_lines(mock_serial, mock_plugin: siemens_serial.SiemensHipathSerial, mocker, raw_line):
    """Test that all sorts of mocked call types work and DO not raise an exception."""
    mock_serial.readline.return_value = raw_line
    spy_push = mocker.patch.object(mock_plugin, "push")
    spy_parse = mocker.patch.object(mock_plugin, "parse")
    spy_validate = mocker.patch.object(mock_plugin, "validate")
    successful = mock_plugin.run()

    assert successful
    assert spy_push.call_count == 1
    assert spy_parse.call_count == 1
    assert spy_validate.call_count == 1
    assert mock_serial.readline.call_count == 1
