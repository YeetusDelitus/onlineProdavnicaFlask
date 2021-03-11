from typing import Tuple
from website import createApp

app = createApp()

if __name__ == '__main__':
    app.run(debug=True)