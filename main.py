from typing import Union
from fastapi import FastAPI, Query, Header
from fastapi.responses import JSONResponse
from pydantic import BaseModel

app = FastAPI()

list_arr = []


class List_things(BaseModel):
    element: str

    def append_element(self):
        list_arr.append(self.element)


class Numbers(BaseModel):
    expr: str
    arr: Union[list[str], None] = None
    num1: Union[int, None] = None
    num2: Union[int, None] = None

    def sep(self):
        try:
            self.arr = (list(map(str, self.expr.split(','))))
            self.num1 = int(self.arr[0])
            self.num2 = int(self.arr[2])
        except ValueError:
            return {"error": "invalid"}
        match self.arr[1]:
            case "+":
                return self.num1 + self.num2
            case "-":
                return self.num1 - self.num2
            case "*":
                return self.num1 * self.num2
            case "/":
                if self.num2 == 0:
                    return {"error": "zerodiv"}
                else:
                    return self.num1 // self.num2
            case _:
                return "Operator does not exist"


@app.get("/sum1n/{n}")
def sum1n(n: int):
    sum1 = 0
    i = 0
    while i < n:
        i += 1
        sum1 = sum1 + i
    return {
        "result": sum1
    }


@app.get("/fibo")
def fibo(n: int = Query("0")):
    fib1 = 1
    fib2 = 1
    i = 0
    while i < n - 3:
        fib_res = fib1 + fib2
        fib1 = fib2
        fib2 = fib_res
        i += 1
    return {
        "result": fib2
    }


@app.post("/reverse")
def reverse(string: str = Header(default=None)):
    newtxt = ''.join(reversed(string))
    return {
        "result": newtxt
    }


@app.put("/list")
def list_put(list: List_things):
    list.append_element()


@app.get("/list")
def list_get():
    return {
        "result": list_arr
    }


@app.post("/calculator")
def calculate(numbers: Numbers):
    result = numbers.sep()
    if result == {"error": "invalid"}:
        return JSONResponse(status_code=400, content={"error": "invalid"})
    elif result == {"error": "zerodiv"}:
        return JSONResponse(status_code=403, content={"error": "zerodiv"})
    elif result == "Operator does not exist":
        return JSONResponse(status_code=400, content={"error": "Operator does not exist"})
    else:
        return {
            "result": result
        }
