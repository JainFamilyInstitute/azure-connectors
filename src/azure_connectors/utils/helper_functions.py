def nice_pass(cls, **kwargs):
    pass_kwargs = {k: v for k, v in kwargs.items() if v is not None}
    return cls(**pass_kwargs)