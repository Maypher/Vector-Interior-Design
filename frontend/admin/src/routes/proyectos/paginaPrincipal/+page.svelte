<script lang="ts">
	import EditorLinks from '$lib/components/layout/editorLinks.svelte';
	import ImageGridMainPage from '$lib/components/layout/imageGridMainPage.svelte';
	import type { PageData } from './$types';

	let { data }: { data: PageData } = $props();
</script>

<div class="size-full bg-black text-white p-20 flex items-center flex-col gap-10">
	<ImageGridMainPage images={data.mainPageData} />
	<div>
		<h1 class="text-2xl text-center">Editor de Página Principal</h1>
		<EditorLinks
			mobileUrl="/proyectos/paginaPrincipal/movil"
			desktopUrl="/proyectos/paginaPrincipal/escritorio"
		/>
	</div>
</div>
