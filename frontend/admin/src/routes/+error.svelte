<script lang="ts">
	import { page } from '$app/state';
</script>

<div
	class="header-screen w-full flex items-center justify-center flex-col text-vector-cream text-3xl font-Nexa"
>
	<h1 class="text-4xl">{page.status}</h1>
	<a href="/cuenta" class="underline"
		>{page.status === 404 ? 'Página no encontrada' : page.error?.message}</a
	>
</div>
