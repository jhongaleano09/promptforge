'use client';

import { useEffect } from 'react';
import { useLanguage } from '@/contexts/LanguageContext';

interface MetadataUpdaterProps {
  children: React.ReactNode;
}

export function MetadataUpdater({ children }: MetadataUpdaterProps) {
  const { t } = useLanguage();

  useEffect(() => {
    document.title = t("app_title");

    const description = document.querySelector('meta[name="description"]');
    if (description) {
      description.setAttribute('content', "Professional Prompt Engineering Tool");
    }

    const html = document.querySelector('html');
    if (html) {
      const lang = document.querySelector('html')?.getAttribute('lang');
      const newLang = t("language_code") === "english" ? "en" : "es";
      if (lang !== newLang) {
        html.setAttribute('lang', newLang);
      }
    }
  }, [t]);

  return <>{children}</>;
}
