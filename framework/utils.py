from retrying import retry
from functools import partial

retry_on_404 = partial(retry,
                       wait_fixed=1500,
                       stop_max_attempt_number=5,
                       retry_on_result=lambda v: v.status == 404,
                       wrap_exception=True)