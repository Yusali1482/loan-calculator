from loan_calculator.cli import main


def test_cli_prints_summary(capsys):
    assert main(["10000", "6", "12"]) == 0
    assert "860.66" in capsys.readouterr().out


def test_cli_schedule_flag_prints_rows(capsys):
    main(["1200", "0", "3", "--schedule"])
    assert "Month" in capsys.readouterr().out


def test_cli_reports_bad_input(capsys):
    assert main(["-5", "6", "12"]) == 1
    assert "Error" in capsys.readouterr().err
