# WoT Hooking
Library for hooking into WoT function calls.

```python
from mod_hooking.strategy import before
from shared_utils.account_helpers.BattleResultsCache import BattleResultsCache

@before(BattleResultsCache, "get")
def before_get(*args, **kwargs):
    print "About to fetch a battle result!"

```