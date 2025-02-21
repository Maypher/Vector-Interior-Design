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

<header
	class="p-3 flex justify-between sticky top-0 z-10 md:static items-center bg-vector-grey h-20"
>
	<div class="flex items-center h-full">
		<a href="/obras/" class="hover:bg-vector-orange p-3 rounded-md transition-colors">Proyectos</a>
		<a href="/obras/paginaPrincipal" class="hover:bg-vector-orange p-3 rounded-md transition-colors"
			>Página Principal</a
		>
		<a href="/obras/esculturas" class="hover:bg-vector-orange p-3 rounded-md transition-colors"
			>Esculturas</a
		>
	</div>
	<button
		type="button"
		{onclick}
		class="m-4 hover:bg-vector-orange hover:brightness-85 p-3 rounded-lg transition-colors cursor-pointer"
	>
		Cerrar Sesión
	</button>
</header>

{@render children()}
