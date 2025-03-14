<script lang="ts">
	import Head from '$lib/components/Head.svelte';
	import { websiteUrl } from '$lib/utilities/constants';
	import logo from '$lib/images/logo.svg';
	import { getI18n } from '$lib/i18n';
	import mdToHtml from '$lib/utilities/markdown';
	import { page } from '$app/state';

	const i18n = getI18n();
</script>

<Head
	title={$i18n.language === 'es' ? 'Conclusión' : 'Conclusion'}
	description={$i18n.t('conclusionBody')}
	url={page.url.toString()}
	alternateEn={`${websiteUrl}/en/proyectos/conclusion`}
	alternateEs={`${websiteUrl}/es/proyectos/conclusion`}
	ogTitle={$i18n.language === 'es' ? 'Conclusión' : 'Conclusion'}
	ogDescription={$i18n.t('conclusionBody')}
	imageUrl={logo}
/>

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
	<a href="mailto:k@vectorinterior.design" class="font-Agency-FB text-2xl font-bold">
		contact@vectorinterior.design
	</a>
</div>
