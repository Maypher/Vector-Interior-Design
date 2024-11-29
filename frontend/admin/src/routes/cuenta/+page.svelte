<script lang="ts">
	import TextInput from '$lib/components/input/TextInput.svelte';
	import PasswordInput from '$lib/components/input/PasswordInput.svelte';
	import { type FormErrors } from '$lib/interfaces';
	import { object, string, ValidationError } from 'yup';
	import { toast } from '@zerodevx/svelte-toast';
	import { goto } from '$app/navigation';

	let loginSchema = object({
		email: string()
			.required('Se require un correo electrónico.')
			.email('Correo electrónico inválido.'),
		password: string().required('Contraseña es requerida.')
	});

	let formData = {
		email: '',
		password: ''
	};

	let errors: FormErrors = $state({});

	async function onsubmit(event: SubmitEvent) {
		event.preventDefault();

		errors = {};

		try {
			let validData = await loginSchema.validate(formData, { abortEarly: false });

			let res = await fetch('/api/auth/iniciar-sesion', {
				method: 'POST',
				body: JSON.stringify(validData),
				headers: {
					'Content-Type': 'application/json'
				}
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

<div class="bg-red-200 w-full max-w-md p-9 rounded-lg">
	<h1 class="text-center">NODO Iniciar Sesión</h1>
	<div class="flex justify-center">
		<form action="POST" {onsubmit} id="form" class="flex flex-col max-w-60">
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
			<button type="submit" class="block bg-blue-100 mt-5 p-2 rounded-lg hover:bg-blue-200">
				Iniciar Sesión
			</button>
		</form>
	</div>
</div>
