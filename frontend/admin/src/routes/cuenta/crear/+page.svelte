<script lang="ts">
	import { ValidationError } from 'yup';
	import TextInput from '$lib/components/input/TextInput.svelte';
	import PasswordInput from '$lib/components/input/PasswordInput.svelte';
	import { type FormErrors } from '$lib/utilities/interfaces';
	import { goto } from '$app/navigation';
	import { signUpForm } from '$lib/utilities/yupSchemas';
	import { error } from '$lib/utilities/toasts';
	import { PUBLIC_apiUrl } from '$env/static/public';

	let formData = {
		name: '',
		email: '',
		password: '',
		passwordRepeat: ''
	};

	let errors: FormErrors = {};

	async function onsubmit(e: SubmitEvent) {
		e.preventDefault();
		errors = {};

		try {
			let validData = await signUpForm.validate(formData, { abortEarly: false });
			let finalData = {
				name: validData.name,
				email: validData.email,
				password: validData.password
			};

			let res = await fetch('http://localhost:8080/auth/crear-cuenta', {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json'
				},
				body: JSON.stringify(finalData)
			});

			if (res.status != 200) {
				let res_msg = await res.text();
				error(res_msg);
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
	<form action="POST" {onsubmit} class="max-w-60">
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
