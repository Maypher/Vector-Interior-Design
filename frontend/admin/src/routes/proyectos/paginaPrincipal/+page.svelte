<script lang="ts">
	import EditorLinks from '$lib/components/layout/editorLinks.svelte';
</script>

<div
	class="size-full bg-black text-white h-[calc(100svh-5rem)] p-20 flex items-center flex-col gap-10"
>
	<h1 class="text-2xl text-center">Editor de Página Principal</h1>
	<EditorLinks
		mobileUrl="/proyectos/paginaPrincipal/movil"
		desktopUrl="/proyectos/paginaPrincipal/escritorio"
	/>
</div>
