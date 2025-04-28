import i18next from "i18next";
import { createI18nStore } from "svelte-i18next";
import type { i18n } from "i18next";
import { type Writable } from "svelte/store";
import { setContext, getContext } from "svelte";



export const setupI18n = async (lang: 'en' | 'es'): Promise<Writable<i18n>> => {
    await i18next.init({
        lng: lang,
        fallbackLng: 'en',
        resources: {
            en: {
                translation: {
                    "english": "English",
                    'Spanish': 'Spanish',
                    'about': 'About Us',
                    'contact': 'Contact',
                    'aboutUsHead': `As a designer,`,
                    'aboutUs': `specialized in Corporate Image and Interior Design, with more than 25 years of experience I'm always on the lookout for new trends, without becoming attached or imposing a style.

Defining the personality of my clients I interpret their needs and aspirations to create spaces that tell their story, achieving an accurate and inimaginable visual impact.

Every project is an opportunity to develop environments with identity and harmony focused on providing comfort, functionality and distinction.I get involved in every single one of its stages, paying close attention to details because they are the ones that mark the difference.”
                    `,
                    'sculptures': 'Sculptures',
                    'projects': 'Projects',
                    'mainPage': 'Main Page',
                    'slogan': `**Tracing lines**
                    **with direction,**
                    **passion and style.**`,
                    'conclusionBody': '**Lines** as a starting and essential element of every design must be focused on a direction molding a frame of reference, the **passion** for transforming and decorating spaces must always aim for quality and confort, considering a set of characteristics that help define a **style** to guarantee in this way exclusivity in the project.',
                    'area': 'Area',
                    "googleDescription": "Specialized in Corporate Image and Interior Design with more than 25 years of experience dedicated to transforming spaces in unique and exclusive environments. Contact: contact@vectorinterior.design"
                }
            },
            es: {
                translation: {
                    'english': "Inglés",
                    'Spanish': 'Español',
                    'about': 'Nosotros',
                    'contact': 'Contacto',
                    'aboutUsHead': `"Como diseñador,`,
                    'aboutUs': `especializado en Imagen Corporativa e Interiorismo, con más de 25 años de experiencia siempre estoy en búsqueda de nuevas tendencias, sin apegarme o imponer un estilo.

Definiendo la personalidad de mis clientes interpreto sus necesidades y aspiraciones para crear espacios que cuenten su historia, logrando un impacto visual certero e inimaginable.

Cada proyecto es una oportunidad para desarrollar ambientes con identidad y armonía enfocados en proporcionar confort, funcionalidad y distinción. Me involucro en cada una de sus etapas, prestando atención minuciosa a los detalles porque son ellos los que marcan la diferencia."`,
                    'sculptures': 'Esculturas',
                    'projects': 'Proyectos',
                    'mainPage': 'Página Principal',
                    'slogan': `**Trazando líneas**
                    **con dirección,**
                    **pasión y estilo.**`,
                    'conclusionBody': "Las **líneas** como elemento inicial y esencial de todo diseño están enfocadas en una **dirección** moldeando un marco de referencia, la **pasión** por transformar y decorar los espacios apunta a la calidad y el confort, considerando un conjunto de características que ayuden a definir un **estilo** para garantizar exclusividad en el proyecto.",
                    'area': 'Área',
                    "googleDescription": "Especializados en Imagen Corporativa y Diseño Interior con más de 25 años de experiencia dedicados a transformar espacios en obras únicas y exclusivas. Contacto: contact@vectorinterior.design"
                }
            }
        },
        interpolation: {
            escapeValue: false, // not needed for svelte as it escapes by default
        }
    });

    return createI18nStore(i18next);
};

const key = 'i18n';


export function setI18n(ctx: Writable<i18n>) { setContext(key, ctx); }
export const getI18n = (): Writable<i18n> => getContext(key);
