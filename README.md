# Easy-Embed Language
## General Information
- Website:
- Documentation:
## Contribution

## TODO
- [ ] Imports
- [ ] Add Some Packages (Like Math)
- [ ] Fix Error Messages for try_register

## Syntax
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
  - ```
    FN map(elements, func)
      VAR new_elements = []
  
      FOR i = 0 TO LEN(elements) THEN
          LS_APPEND(new_elements, func(elements^i))
      END
  
      RETURN new_elements
    END
    ```
  - ```
    FN add(a, b) -> a + b
    ```
- **Variables:**
  - ```VAR a = "Hello"```
  - ```VAR b = 2```
  - ```VAR c = 2.756```
  - ```VAR d = map  # See above map function```
- **Comments:** ```# This is a comment```
