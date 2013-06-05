# TODO

## General points

  - Threading:
    - GUI needs to be a seperate thread
    - exchange system is a seperate thread
    - updater is a seperate thread and locks the GUI when active
  - how many digits after the comma? 8?

  - no update when a transaction is active - Done, handled by state = 'idle|update|trade'

## GUI

  - Mainmenu:
    - BTC -> EUR
    - EUR -> BTC
    - Help
  - BTC -> EUR and EUR -> BTC menus:
    - amount [0.000]
    - fee [0.000]
    - c-base donation [0.000] [x]
    - btc-o-matic donation [0.000] [x]
    - total BTC [0.000]
    - total EUR [0.000]
    - keypad with [0-9.], [Backspace], [Trade], [Cancel]
  - always on screen:
    - ask
    - bid
    - if in admin/maintenance mode:
      - amount of BTC and EUR in the btc-o-matic
