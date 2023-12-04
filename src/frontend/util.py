import functools


def centered(cls):
    """Centers a TKinter window on the screen. `cls` should have WIDTH and HEIGHT atributes, which can be None."""

    @functools.wraps(cls)
    def wrapper(*args, **kwargs):
        wrapper = cls(*args, **kwargs)
        SCRN_WIDTH, SCRN_HEIGHT = (
            wrapper.winfo_screenwidth(),
            wrapper.winfo_screenheight(),
        )
        if not wrapper.WIDTH:
            WIDTH = wrapper.winfo_width()
        else:
            WIDTH = wrapper.WIDTH
        if not wrapper.HEIGHT:
            HEIGHT = wrapper.winfo_height()
        else:
            HEIGHT = wrapper.HEIGHT

        wrapper.geometry(
            "{}x{}+{}+{}".format(
                WIDTH,
                HEIGHT,
                (SCRN_WIDTH // 2 - WIDTH // 2),
                (SCRN_HEIGHT // 2 - HEIGHT // 2),
            )
        )
        return wrapper

    return wrapper
