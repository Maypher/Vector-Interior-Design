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
	import { PUBLIC_apiURL, PUBLIC_userFrontendURL } from '$env/static/public';
	import logo from '$lib/images/logo.svg';
	import { onMount } from 'svelte';

	const { data }: { data: PageData } = $props();
	const { form, errors, constraints, enhance } = superForm(data.loginForm, {
		SPA: true,
		validators: yup(loginSchema),
		resetForm: false,
		async onUpdate({ form }) {
			submitting = true;

			if (form.valid) {
				const res = await fetch(`https://${PUBLIC_apiURL}/auth/iniciar-sesion`, {
					method: 'POST',
					body: objectToFormData(form.data),
					credentials: 'include'
				});

				if (res.ok) {
					await goto(`/proyectos/`);
				} else {
					const errorMsg = await res.text();
					error(errorMsg);
				}
			}

			submitting = false;
		}
	});

	let submitting: boolean = $state(false);

	onMount(async () => {
		const alreadyLoggedIn = (
			await fetch(`https://${PUBLIC_apiURL}/auth/info-usuario`, {
				credentials: 'include'
			})
		).ok;
		if (alreadyLoggedIn) goto('/proyectos');
	});
</script>

<div
	class=" bg-vector-cream/40 backdrop-blur-xl w-full max-w-md p-10 md:rounded-lg shadow-lg shadow-vector-cream"
>
	<img src={logo} alt="Logo" class="w-1/2 mx-auto" />
	<div class="flex justify-center">
		<form id="form" class="flex flex-col max-w-60" use:enhance onsubmit={(e) => e.preventDefault()}>
			<fieldset disabled={submitting} class="text-white">
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
					class="block bg-gray-500 mt-5 p-2 rounded-lg hover:bg-gray-700 transition-colors cursor-pointer disabled:cursor-not-allowed"
				>
					Iniciar Sesión
				</button>
			</fieldset>
		</form>
	</div>

	<p class="mt-10 text-vector-black text-balance">
		Esta página esta destinada para administradores. Si no eres un administrador por favor
		<a href={`https://${PUBLIC_userFrontendURL}`} class="text-vector-orange underline">
			regresa a la página principal
		</a>.
	</p>
</div>
