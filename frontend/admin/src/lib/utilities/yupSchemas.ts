import { object, string, ref } from "yup";

export const loginSchema = object({
    email: string()
        .required('Se require un correo electrónico.')
        .email('Correo electrónico inválido.'),
    password: string().required('Contraseña es requerida.')
});


export const signUpForm = object({
    name: string().required('Nombre requerido'),
    email: string().required('Correo electrónico requerido.').email('Correo invalido'),
    password: string()
        .required('Contraseña es requerida.')
        .min(8, 'Contraseña debe tener al menos 8 caracteres.')
        .matches(
            /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*(),.?":{}|<>])[A-Za-z\d!@#$%^&*(),.?":{}|<>]{8,}$/,
            'Contraseña debe contener al menos una letra mayúscula, una minúscula, un número y un símbolo.'
        ),
    passwordRepeat: string()
        .required('Confirmar contraseña.')
        .oneOf([ref('password')], 'Contraseñas no coinciden.')
});
