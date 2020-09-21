from kakao.parser import get_code, remove_korean


def test_get_code1():
    assert get_code('nickname b0fd9698') == 'b0fd9698'


def test_get_code2():
    assert get_code('b0fd9698 부두술사') == 'b0fd9698'


def test_get_code3():
    assert get_code('주식보조 고따따(b0fd9698)') == 'b0fd9698'


def test_get_code4():
    assert get_code('염재호.(37228270)') == '37228270'
    assert get_code('727116cd') == '727116cd'
    assert get_code('바쁜벌꿀d536a608') == 'd536a608'


def test_get_code5():
    assert get_code('jyp abyss(09fdcd94)') == '09fdcd94'
    assert get_code('[b7003ba3]구닌아저씨') == 'b7003ba3'
    assert get_code('바닥/6aca40e5') == '6aca40e5'
    assert get_code('새신랑(86623e5b') == '86623e5b'
    assert get_code('65c2e5ed.하루1퍼 가즈아') == '65c2e5ed'
    assert get_code('(배가)고파서(f68383ee)') == 'f68383ee'
    assert get_code('가하멘...10686eea') == '10686eea'


def test_remove_korean1():
    assert remove_korean('염재호.(37228270)') == '.(37228270)'
    assert remove_korean('바쁜벌꿀d536a608') == 'd536a608'


def test_remove_korean2():
    assert remove_korean('d536a608바쁜벌꿀') == 'd536a608'
    assert remove_korean('주식보조 고따따(b0fd9698)') == '(b0fd9698)'
