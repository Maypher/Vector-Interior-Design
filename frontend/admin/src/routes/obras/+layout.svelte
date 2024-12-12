<script>
	import { redirect } from '@sveltejs/kit';

	let { children } = $props();

	async function onclick() {
		let res = await fetch('/api/auth/cerrar-sesion', {
			method: 'POST'
		});

		if (res.status == 200) redirect(302, '/cuenta/');
	}
</script>

<header class="p-3 flex justify-end align-middle bg-gray-400">
	<button type="button" {onclick} class="m-4 hover:bg-blue-400 p-3 rounded-lg">
		Cerrar Sesión
	</button>
</header>

{@render children()}
