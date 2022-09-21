// Version 1.0
get_suma = (n_fields) => {
    suma = 0;
    for (let i=1; i<=n_fields; i++){
        let value = document.getElementById("field"+i).value;
        if (value != ""){
            suma += parseInt(value, 10);
        }
    }
    return suma;
}

set_invalid = (field) => {
    field.classList.remove("is-valid");
    field.classList.add("is-invalid");
}

set_valid = (field) => {
    field.classList.remove("is-invalid");
    field.classList.add("is-valid");
}