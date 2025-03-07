<script lang="ts">
	import logo from '$lib/images/logo.svg';
	import { getI18n } from '$lib/i18n';
	import mdToHtml from '$lib/utilities/markdown';

	const i18n = getI18n();
</script>

<div
	class="bg-vector-grey flex h-screen w-screen flex-col items-center justify-center gap-20 overflow-x-clip p-10"
>
	<a href={`/${$i18n.language}`} class="transition-transform will-change-transform hover:scale-110">
		<img src={logo} alt="Vector: Interior Design" class="w-64" />
	</a>
	<h1 class="text-4xl"><b>{$i18n.t('conclusionHeader')}</b></h1>
	<div id="conclusion" class="text-center indent-5 text-xl">
		{@html mdToHtml($i18n.t('conclusionBody'))}
	</div>
</div>
