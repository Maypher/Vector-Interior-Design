<script>
	import { redirectWithToast } from '$lib/utilities/toasts';

	let { children } = $props();

	async function onclick() {
		let res = await fetch('/api/auth/cerrar-sesion', {
			method: 'POST'
		});

		if (res.status == 200) redirectWithToast('/cuenta', 'Cierre de sesión exitoso.', 'SUCCESS');
	}
</script>

<header class="p-3 flex justify-end align-middle bg-gray-400">
	<button type="button" {onclick} class="m-4 hover:bg-blue-400 p-3 rounded-lg">
		Cerrar Sesión
	</button>
</header>

{@render children()}
