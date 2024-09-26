import time
from functions import get_data
from IPython.display import clear_output

if __name__ == '__main__':
  while True:
          clear_output(wait=True)
          get_data()
          time.sleep(60)