import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt

def main():
    data = pd.Series([0.25, 0.5, 0.75, 1.0])
    print('data')
    print(data)

if __name__ == '__main__':
    print('Python version ' + sys.version)
    print('Pandas version ' + pd.__version__)
    print('Matplotlib version ' + matplotlib.__version__)

    argc = len(sys.argv)
    main()
    sys.exit(0)
