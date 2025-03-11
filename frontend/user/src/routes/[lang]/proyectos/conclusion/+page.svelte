<script lang="ts">
	import logo from '$lib/images/logo.svg';
	import { getI18n } from '$lib/i18n';
	import mdToHtml from '$lib/utilities/markdown';

	const i18n = getI18n();
</script>

<div
	class="flex h-screen w-screen flex-col items-center justify-center gap-20 overflow-x-clip bg-[#989898] p-10"
>
	<a href={`/${$i18n.language}`} class="transition-transform will-change-transform hover:scale-110">
		<img src={logo} alt="Vector: Interior Design" class="w-64" />
	</a>
	<h1 class="text-center text-3xl">{$i18n.t('conclusionHeader')}</h1>
	<div
		id="conclusion"
		class="whitespace-normal text-center indent-5 text-xl [&_br]:hidden lg:[&_br]:block"
	>
		{@html mdToHtml($i18n.t('conclusionBody'))}
	</div>
	<a href="mailto:k@vectorinterior.design" class="font-Agency-FB text-3xl font-bold">
		contact@vectorinterior.design
	</a>
</div>
