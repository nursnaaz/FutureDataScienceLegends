from zenml import pipeline, step
import sys

@step
def step_1(txt: str) -> str:
    res = "Text:" + txt
    print('in  step1: ', res)
    return res

@pipeline
def my_pipeline(txt: str) -> None:
    response = step_1(txt)

if __name__ == "__main__":
    #new_txt = 'MyZen'
    print(len(sys.argv))
    if len(sys.argv) == 2:
        new_txt = sys.argv[1]
        my_pipeline(new_txt)
    else:
        print('Usage: python test1.py <newtext>')


