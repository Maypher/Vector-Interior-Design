import { object, string, ref, number } from "yup";

export const loginSchema = object({
    email: string()
        .required('Se require un correo electrónico.')
        .email('Correo electrónico inválido.'),
    password: string().required('Contraseña es requerida.')
});


export const signUpForm = object({
    name: string().required('Nombre requerido.'),
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

export const obraCreateSchema = object({
    name: string().required("Nombre requerido.").min(5, "Nombre debe tener un mínimo de 5 caracteres"),
    area: number().default(1).min(1, "El debe ser mayor a cero."),
    description: string().required("Descripción requerida.")
})

export const ambienteCreateSchema = object({
    name: string().required("Nombre requerido.").min(4, "Nombre debe tener un mínimo de 4 caracteres"),
    description: string().default('')
});

export const imageUpdateSchema = object({
    altText: string().required("Texto alternativo requerido."),
});
