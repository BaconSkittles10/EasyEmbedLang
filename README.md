# Easy-Embed Language
## General Information
- Website:
- Documentation:
## Contribution

## TODO
- [ ] Classes
- [ ] Package Manager or Remote Install Packages from Github
- [ ] -= and += operators
- [ ] event Keyword (like in C#)
  - This will look like ```EVENT myevent```
  - ```myevent.subscribe(func)``` OR ```myevent += func```
  - ```myevent.unsubscribe(func)``` OR ```myevent -= func```
  - ```myevent.invoke()```

## Syntax
- **Imports:**
  - First, it attempts to import a file using the relative path or filename provided. Then it tries to find it in the built-in Libs.
  - ```IMPORT "math"```
  - ```IMPORT "localfile"```
  - ```IMPORT "subdir/anotherfile"```
  - **Do not include the file extension in your import**
  - To use a function or variable from another file use ```filename::itemname```
- **Loops:**
  - ```
    FOR i = 0 TO 6 THEN
      PRINT("Iteration " + i)
    END
    ```
  - ```
    WHILE x < 6 THEN
      PRINT("Iteration " + x)
      x = x + 1
    END
    ```
- **Functions:**
  - Multi-line functions (does not have to return a value):
    ```
    FN map(elements, func)
      VAR new_elements = []
  
      FOR i = 0 TO LEN(elements) THEN
          LS_APPEND(new_elements, func(elements^i))
      END
  
      RETURN new_elements
    END

    map([1, 2, 3, 4, 5], math::double)  # Must import "math"; doubles all the elements
    ```
  - Single line functions (automatically returns the calculated value):
     ```
    FN add(a, b) -> a + b
    add(1, 2)  # 3
    ```
- **Variables:**
  - ```VAR a = "Hello"```
  - ```VAR b = 2```
  - ```VAR c = 2.756```
  - ```VAR d = map  # See above map function```
  - ```VAR e = [1, 2, 3, "hi", "test"]```
  - ```VAR f = {"key": val, 1: "test", 2: 3}```
- **Comments:** ```# This is a comment```
