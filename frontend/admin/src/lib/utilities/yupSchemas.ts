import { object, string, number, bool } from "yup";

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
});

export const projectCreateSchema = object({
    name: string().required("Nombre requerido.").min(5, "Nombre debe tener un mínimo de 5 caracteres"),
    area: number().default(1).min(1, "El debe ser mayor a cero."),
    descriptionEs: string().required("Descripción requerida."),
    descriptionEn: string().required("Descripción en ingles requerida")
})

export const spaceCreateSchema = object({
    name: string().required("Nombre requerido.").min(4, "Nombre debe tener un mínimo de 4 caracteres"),
    description: string().default('')
});

export const createImageSchema = object({
    altTextEs: string().required("Texto alternativo requerido.").length(255),
    altTextEn: string().required("Texto alternativo en ingles requerido.").length(255)
});

export const imageUpdateSchema = object({
    altTextEs: string().required("Texto alternativo requerido."),
    altTextEn: string().required("Text alternativo en ingles requerido."),
    descriptionEs: string(),
    descriptionEn: string(),
    descriptionFont: string().required("Fuente de descripción requerida."),
    hideInProject: bool(),
    sculpture: bool()
});
