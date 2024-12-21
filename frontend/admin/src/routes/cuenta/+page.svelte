<script lang="ts">
	import TextInput from '$lib/components/input/TextInput.svelte';
	import PasswordInput from '$lib/components/input/PasswordInput.svelte';
	import objectToFormData from '$lib/utilities/formData';
	import { superForm } from 'sveltekit-superforms';
	import type { PageData } from './$types';
	import { yup } from 'sveltekit-superforms/adapters';
	import { loginSchema } from '$lib/utilities/yupSchemas';
	import { goto } from '$app/navigation';
	import { error } from '$lib/utilities/toasts';
	import { PUBLIC_apiURL } from '$env/static/public';

	const { data }: { data: PageData } = $props();
	const { form, errors, constraints, enhance } = superForm(data.loginForm, {
		SPA: true,
		validators: yup(loginSchema),
		resetForm: false,
		async onUpdate({ form }) {
			submitting = true;

			if (form.valid) {
				const res = await fetch(`${PUBLIC_apiURL}auth/iniciar-sesion`, {
					method: 'POST',
					body: objectToFormData(form.data),
					credentials: 'include'
				});

				if (res.ok) {
					await goto(`/obras/`);
				} else {
					const errorMsg = await res.text();
					error(errorMsg);
				}
			}

			submitting = false;
		}
	});

	let submitting: boolean = $state(false);
</script>

<div class="bg-red-200 w-full max-w-md p-9 rounded-lg">
	<h1 class="text-center">NODO Iniciar Sesión</h1>
	<div class="flex justify-center">
		<form action="POST" id="form" class="flex flex-col max-w-60" use:enhance>
			<fieldset disabled={submitting}>
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
					{...$constraints.password}
				/>
				<button
					type="submit"
					class="block bg-blue-100 mt-5 p-2 rounded-lg hover:bg-blue-200 disabled:cursor-not-allowed"
				>
					Iniciar Sesión
				</button>
			</fieldset>
		</form>
	</div>
</div>
