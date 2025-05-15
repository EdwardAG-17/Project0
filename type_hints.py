my_string_variable = "my string variable"
print(my_string_variable)
print(type(my_string_variable))

#Python es un lenguaje de tipo dinamico, si volvemos a marcar la variable con otro valor, cambiará
my_string_variable = 4
print(my_string_variable)
print(type(my_string_variable))

#TYPE HINTS o anotacion de texto es una sintexis especial que busca declarar el tipo de valor que es la variable.
my_typed_variable: str = "My typed string variable"
print(my_typed_variable)
print(type(my_typed_variable))

#Python tiene este tipado debil, si marcamos el int (5), como str lo entendera asi en el programa pero en la terminal
#a pesar de haberle declarado str, lo seguira entendiendo como un int.
my_typed_variable: str = 5
print(my_typed_variable)
print(type(my_typed_variable))
