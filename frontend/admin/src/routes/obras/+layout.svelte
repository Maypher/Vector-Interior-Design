<script>
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

<header class="p-3 flex justify-between items-center bg-gray-400">
	<a href="/obras/" class="hover:bg-red-500 p-3 rounded-md"
		><span class="material-symbols-outlined text-4xl"> home </span></a
	>
	<button type="button" {onclick} class="m-4 hover:bg-blue-400 p-3 rounded-lg">
		Cerrar Sesión
	</button>
</header>

{@render children()}
