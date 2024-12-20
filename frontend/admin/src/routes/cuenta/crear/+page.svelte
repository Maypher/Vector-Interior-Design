<script lang="ts">
	import { ValidationError } from 'yup';
	import TextInput from '$lib/components/input/TextInput.svelte';
	import PasswordInput from '$lib/components/input/PasswordInput.svelte';
	import { goto } from '$app/navigation';
	import { signUpForm } from '$lib/utilities/yupSchemas';
	import { error } from '$lib/utilities/toasts';
	import type { PageData } from './$types';
	import { setError, superForm } from 'sveltekit-superforms';
	import { yup } from 'sveltekit-superforms/adapters';

	const { data }: { data: PageData } = $props();

	const { form, errors, constraints, enhance } = superForm(data.createForm, {
		SPA: true,
		resetForm: false,
		validators: yup(signUpForm),
		async onUpdate({ form }) {
			if (form.valid) {
				// Done this way because using ref in the yup schema creates a nested value
				// and superform complains that its a nested value.
				if (form.data.password !== form.data.passwordRepeat) {
					setError(form, 'passwordRepeat', 'Constraseñas no coinciden');
					return;
				}

				let formData = new FormData();

				formData.append('email', form.data.email);
				formData.append('password', form.data.password);
				formData.append('name', form.data.name);

				let res = await fetch('http://localhost:8080/auth/crear-cuenta', {
					method: 'POST',
					body: formData
				});

				if (res.ok) await goto('/obras/');
				else error(await res.text());
			}
		}
	});
</script>

<div class="bg-blue-400 rounded-lg flex flex-col justify-center p-9">
	<h1 class="text-center">NODO Crear Cuenta</h1>
	<form action="POST" class="max-w-60" use:enhance>
		<TextInput
			name="name"
			label="Nombre"
			type="text"
			bind:value={$form.name}
			errors={$errors.name}
			{...$constraints.name}
		/>
		<TextInput
			name="email"
			label="Correo Electrónico"
			type="text"
			bind:value={$form.email}
			errors={$errors.email}
			{...$constraints.email}
		/>
		<PasswordInput
			name="password"
			label="Contraseña"
			bind:value={$form.password}
			errors={$errors.password}
		/>
		<!-- Not adding constrains here because js regex doesn't play nicely with HTML regex -->
		<PasswordInput
			name="passwordRepeat"
			label="Confirmar contraseña"
			bind:value={$form.passwordRepeat}
			errors={$errors.passwordRepeat}
		/>
		<button class="bg-green-500 rounded-lg p-2">Crear Cuenta</button>
	</form>
</div>
