<script lang="ts">
	import { object, string, ref, ValidationError } from 'yup';
	import TextInput from '$lib/components/input/TextInput.svelte';
	import PasswordInput from '$lib/components/input/PasswordInput.svelte';
	import { type FormErrors } from '$lib/interfaces';
	import { toast } from '@zerodevx/svelte-toast';
	import { goto } from '$app/navigation';

	let signUpForm = object({
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

	let formData = {
		name: '',
		email: '',
		password: '',
		passwordRepeat: ''
	};

	let errors: FormErrors = {};

	async function onsubmit(e: SubmitEvent) {
		e.preventDefault();

		try {
			let validData = await signUpForm.validate(formData, { abortEarly: false });
			let finalData = {
				name: validData.name,
				email: validData.email,
				password: validData.password
			};

			let res = await fetch('/api/auth/crear-cuenta', {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json'
				},
				body: JSON.stringify(finalData)
			});

			if (res.status != 200) {
				let res_msg = await res.text();
				toast.push(res_msg, {
					theme: {
						'--toastBackground': 'red',
						'--toastBarBackground': '#7f0000'
					}
				});
			} else {
				goto('/panel');
			}
		} catch (err) {
			(err as ValidationError).inner.forEach((e) => {
				const errorField = e.path;

				if (errorField) {
					if (errors[errorField]) {
						errors[errorField].push(...e.errors);
					} else {
						errors[errorField] = e.errors;
					}
				}
			});
		}
	}
</script>

<div class="bg-blue-400 rounded-lg flex flex-col justify-center p-9">
	<h1 class="text-center">NODO Crear Cuenta</h1>
	<form action="POST" {onsubmit}>
		<TextInput
			name="name"
			label="Nombre"
			type="text"
			bind:value={formData.name}
			errors={errors['name']}
		/>
		<TextInput
			name="email"
			label="Correo Electrónico"
			type="text"
			bind:value={formData.email}
			errors={errors['email']}
		/>
		<PasswordInput
			name="password"
			label="Contraseña"
			bind:value={formData.password}
			errors={errors['password']}
		/>
		<PasswordInput
			name="passwordRepeat"
			label="Confirmar contraseña"
			bind:value={formData.passwordRepeat}
			errors={errors['passwordRepeat']}
		/>
		<button class="bg-green-500 rounded-lg p-2">Crear Cuenta</button>
	</form>
</div>
