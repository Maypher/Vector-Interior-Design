<script>
	import { goto } from '$app/navigation';
	import { PUBLIC_apiURL } from '$env/static/public';

	let { children } = $props();

	async function onclick() {
		let res = await fetch(`${PUBLIC_apiURL}auth/cerrar-sesion`, {
			method: 'POST',
			credentials: 'include'
		});

		if (res.ok) goto('/cuenta/');
	}
</script>

<header class="p-3 flex justify-between items-center bg-gray-400 h-20">
	<div class="flex items-center h-full">
		<a href="/obras/" class="hover:bg-red-500 p-3 rounded-md">Proyectos</a>
		<a href="/obras/paginaPrincipal" class="hover:bg-red-500 p-3 rounded-md">Página Principal</a>
	</div>
	<button type="button" {onclick} class="m-4 hover:bg-blue-400 p-3 rounded-lg">
		Cerrar Sesión
	</button>
</header>

{@render children()}
