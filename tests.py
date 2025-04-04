import pytest
from model import Question


def test_create_question():
    question = Question(title='q1')
    assert question.id != None


def test_create_multiple_questions():
    question1 = Question(title='q1')
    question2 = Question(title='q2')
    assert question1.id != question2.id


def test_create_question_with_invalid_title():
    with pytest.raises(Exception):
        Question(title='')
    with pytest.raises(Exception):
        Question(title='a'*201)
    with pytest.raises(Exception):
        Question(title='a'*500)


def test_create_question_with_valid_points():
    question = Question(title='q1', points=1)
    assert question.points == 1
    question = Question(title='q1', points=100)
    assert question.points == 100


def test_create_choice():
    question = Question(title='q1')

    question.add_choice('a', False)

    choice = question.choices[0]
    assert len(question.choices) == 1
    assert choice.text == 'a'
    assert not choice.is_correct


def test_create_question_with_invalid_point():
    with pytest.raises(Exception):
        Question(title='Test', points=101)
    with pytest.raises(Exception):
        Question(title='Test', points=0)


def test_create_choice_with_invalid_text():
    question = Question(title='Test')

    with pytest.raises(Exception):
        question.add_choice('', False)
    with pytest.raises(Exception):
        question.add_choice('a'*120, False)


def test_remove_valid_choice():
    question = Question(title='Test')

    question.add_choice('a', False)
    assert len(question.choices) == 1

    choice = question.choices[0]
    question.remove_choice_by_id(choice.id)
    assert len(question.choices) == 0


def test_remove_invalid_choice():
    question = Question(title='Test')

    question.add_choice('a', False)
    assert len(question.choices) == 1

    with pytest.raises(Exception):
        question.remove_choice_by_id('invalid_id')


def test_remove_all_choices():
    question = Question(title='Test')
    question.add_choice('a', False)
    question.add_choice('b', False)
    assert len(question.choices) == 2

    question.remove_all_choices()
    assert len(question.choices) == 0


def test_select_choices():
    question = Question(title='Test', max_selections=2)
    question.add_choice('a', True)
    question.add_choice('b', True)
    question.add_choice('c', False)

    selected_choices = question.select_choices(
        [question.choices[0].id, question.choices[1].id])
    assert len(selected_choices) == 2
    assert selected_choices[0] == question.choices[0].id
    assert selected_choices[1] == question.choices[1].id


def test_select_choices_wrong_choice():
    question = Question(title='Test', max_selections=2)
    question.add_choice('b', False)

    selected_choices = question.select_choices(
        [question.choices[0].id])
    assert len(selected_choices) == 0


def test_select_choices_exceed_max_selections():
    question = Question(title='Test', max_selections=1)
    question.add_choice('a', True)
    question.add_choice('b', True)

    with pytest.raises(Exception):
        question.select_choices(
            [question.choices[0].id, question.choices[1].id])


def test_set_correct_choices():
    question = Question(title='Test')
    question.add_choice('a', False)
    question.add_choice('b', False)

    question.set_correct_choices([question.choices[0].id])
    assert question.choices[0].is_correct
    assert not question.choices[1].is_correct


def test_set_correct_choices_invalid_choice():
    question = Question(title='Test')
    question.add_choice('a', False)
    question.add_choice('b', False)

    with pytest.raises(Exception):
        question.set_correct_choices(['invalid_id'])
