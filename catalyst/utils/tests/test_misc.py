import torch.nn as nn

from catalyst import utils


def test_get_fn_argsnames():
    class Net1(nn.Module):
        def forward(self, x):
            return x

    class Net2(nn.Module):
        def forward(self, x, y):
            return x

    class Net3(nn.Module):
        def forward(self, x, y=None):
            return x

    class Net4(nn.Module):
        def forward(self, x, *, y=None):
            return x

    class Net5(nn.Module):
        def forward(self, *, x):
            return x

    class Net6(nn.Module):
        def forward(self, *, x, y):
            return x

    class Net7(nn.Module):
        def forward(self, *, x, y=None):
            return x

    nets = [Net1, Net2, Net3, Net4, Net5, Net6, Net7]
    params_true = [
        ["x"],
        ["x", "y"],
        ["x", "y"],
        ["x", "y"],
        ["x"],
        ["x", "y"],
        ["x", "y"],
    ]

    params_predicted = list(
        map(
            lambda x: utils.get_fn_argsnames(x.forward, exclude=["self"]), nets
        )
    )
    assert params_predicted == params_true


def test_fn_ends_with_pass():
    def useless_fn():
        pass

    def useless_fn_with_newline_between_signature_and_pass():

        pass

    def useless_fn_with_docstring():
        """
            Docstring yay
        """
        pass

    def useless_fn_with_multiline_signature(
            first_arg=None,
            second_arg: "Any" = None,
    ):
        pass

    def useless_fn_with_multiline_signature_and_docstring(
            first_arg=None,
            second_arg: "Any" = None,
    ):
        """
            Docstring yay
        """
        pass

    def usefull_fn():
        print("I am useful!")

    assert utils.fn_ends_with_pass(useless_fn) is True
    assert utils.fn_ends_with_pass(useless_fn_with_newline_between_signature_and_pass) is True
    assert utils.fn_ends_with_pass(useless_fn_with_docstring) is True
    assert utils.fn_ends_with_pass(useless_fn_with_multiline_signature) is True
    assert utils.fn_ends_with_pass(useless_fn_with_multiline_signature_and_docstring) is True
    assert utils.fn_ends_with_pass(usefull_fn) is False