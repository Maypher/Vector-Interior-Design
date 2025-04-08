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
                    'aboutUsHead': `As an interior
                    *designer,*`,
                    'aboutUs': "From sublime to majestic, the limit of this designer is infinite. Defining his client's personality he's capable of converting the most simple of spaces to unique and exclusive works, achieving an accurate and sometimes inimaginable visual aspect.",
                    'sculptures': 'Sculptures',
                    'projects': 'Projects',
                    'mainPage': 'Main Page',
                    'sculptureHeader': 'Unique and exclusive works',
                    'conclusionHeader': `Tracing lines with direction, passion, and style.`,
                    'conclusionBody': '**Lines** as a starting and essential element of every design must be focused\n on a direction molding a frame of reference, the **passion** for transforming and\n decorating spaces must always aim for quality and confort, considering\n a set of characteristics that help define a **style** to guarantee in this way\n exclusivity in the project.',
                    'slogan': 'Being different has its advantages',
                    'area': 'Area',
                    'areaUnits': 'm²'
                }
            },
            es: {
                translation: {
                    'english': "Ingles",
                    'Spanish': 'Español',
                    'about': 'Nosotros',
                    'contact': 'Contacto',
                    'aboutUsHead': `Como diseñador 
                de *interiores*,`,
                    'aboutUs': `con más de 25 años de experiencia siempre estoy en la búsqueda de nuevas tendencias, sin apegarme o imponer un estilo, definiendo la personalidad de mis clientes interpreto sus necesidades y aspiraciones para crear espacios que cuenten su historia, logrando un impacto visual certero e inimaginable.
 
Cada proyecto es una oportunidad para crear ambientes con identidad y armonía, proporcionando confort, funcionalidad y distinción. Me involucro en cada una de sus etapas, prestando atención minuciosa a los detalles porque son ellos los que marcan la diferencia.`,
                    'sculptures': 'Esculturas',
                    'projects': 'Proyectos',
                    'mainPage': 'Página Principal',
                    'sculptureHeader': 'Obras únicas y exclusivas',
                    'conclusionHeader': 'Trazando líneas con dirección, pasión y estilo.',
                    'conclusionBody': `Las **líneas** como elemento inicial y esencial de todo diseño están enfocadas en una **dirección** moldeando un marco de referencia, la **pasión** por transformar y decorar los espacios apunta a la calidad y el confort, considerando un conjunto de características que ayuden a definir un **estilo** para garantizar exclusividad en el proyecto.`,
                    'slogan': `**Trazando líneas**
                    **con dirección,**
                    **pasión y estilo.**`,
                    'area': 'Área',
                    'areaUnits': 'm²',
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
