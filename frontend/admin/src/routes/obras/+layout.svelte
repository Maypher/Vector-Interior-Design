<script>
	import { redirect } from '@sveltejs/kit';
	import { PUBLIC_apiUrl } from '$env/static/public';
	import { goto } from '$app/navigation';

	let { children } = $props();

	async function onclick() {
		let res = await fetch('http://localhost:8080/auth/cerrar-sesion', {
			method: 'POST',
			credentials: 'include'
		});

		if (res.ok) goto('/cuenta/');
	}
</script>

<header class="p-3 flex justify-end align-middle bg-gray-400">
	<button type="button" {onclick} class="m-4 hover:bg-blue-400 p-3 rounded-lg">
		Cerrar Sesión
	</button>
</header>

{@render children()}
