try:
    from debug_utils import LOG_CURRENT_EXCEPTION
except ImportError:
    import traceback

    def LOG_CURRENT_EXCEPTION():
        traceback.print_exc()
