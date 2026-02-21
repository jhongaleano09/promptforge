'use client';

import { useState, useEffect } from 'react';
import { BookOpen, Star, Search, Filter, ChevronDown, ChevronUp } from 'lucide-react';
import { useLanguage } from '@/contexts/LanguageContext';
import { API_BASE } from '@/config/api';

interface PromptTemplate {
  id: number;
  type: string;
  name: string;
  description: string;
  category: string;
  tags: string[];
  usage_count: number;
}

interface TemplateLibraryProps {
  promptType?: 'basic' | 'system' | 'image' | 'additional';
  onTemplateSelect?: (templateId: number, templateContent: string) => void;
}

export function TemplateLibrary({ promptType, onTemplateSelect }: TemplateLibraryProps) {
  const { t } = useLanguage();
  const [templates, setTemplates] = useState<PromptTemplate[]>([]);
  const [loading, setLoading] = useState(true);
  const [selectedCategory, setSelectedCategory] = useState<string>('all');
  const [searchQuery, setSearchQuery] = useState('');
  const [expandedTemplate, setExpandedTemplate] = useState<number | null>(null);

  useEffect(() => {
    fetchTemplates();
  }, [promptType]);

  const fetchTemplates = async () => {
    setLoading(true);
    try {
      const url = promptType
        ? `${API_BASE}/prompts/templates/type/${promptType}`
        : `${API_BASE}/prompts/templates`;

      const res = await fetch(url);
      const data = await res.json();
      setTemplates(data.templates || []);
    } catch (error) {
      console.error('Error loading templates:', error);
    } finally {
      setLoading(false);
    }
  };

  const categories = ['all', ...new Set(templates.map(t => t.category))];

  const filteredTemplates = templates.filter(template => {
    const matchesCategory = selectedCategory === 'all' || template.category === selectedCategory;
    const matchesSearch = searchQuery === '' ||
      template.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
      template.description.toLowerCase().includes(searchQuery.toLowerCase()) ||
      template.tags.some(tag => tag.toLowerCase().includes(searchQuery.toLowerCase()));

    return matchesCategory && matchesSearch;
  });

  const handleTemplateClick = async (template: PromptTemplate) => {
    if (expandedTemplate === template.id) {
      setExpandedTemplate(null);
    } else {
      setExpandedTemplate(template.id);
    }
  };

  const handleUseTemplate = async (template: PromptTemplate) => {
    try {
      await fetch(`${API_BASE}/prompts/templates/${template.id}/use`, {
        method: 'POST',
      });

      if (onTemplateSelect) {
        onTemplateSelect(template.id, template.name);
      }
    } catch (error) {
      console.error('Error using template:', error);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center p-8">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary"></div>
      </div>
    );
  }

  return (
    <div className="max-w-6xl mx-auto p-4">
      <div className="mb-6">
        <h2 className="text-2xl font-bold mb-2">{t('template_library_title')}</h2>
        <p className="text-muted-foreground">{t('template_library_description')}</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
        <div>
          <label className="block text-sm font-medium mb-2">{t('category')}</label>
          <div className="relative">
            <select
              value={selectedCategory}
              onChange={(e) => setSelectedCategory(e.target.value)}
              className="w-full px-4 py-2 pr-10 border rounded-lg appearance-none bg-background"
            >
              <option value="all">{t('all_categories')}</option>
              {categories.filter(cat => cat !== 'all').map(category => (
                <option key={category} value={category}>{category}</option>
              ))}
            </select>
            <ChevronDown className="absolute right-3 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground pointer-events-none" />
          </div>
        </div>

        <div className="md:col-span-2">
          <label className="block text-sm font-medium mb-2">{t('search')}</label>
          <div className="relative">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground" />
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder={t('search_templates')}
              className="w-full pl-10 pr-4 py-2 border rounded-lg bg-background"
            />
          </div>
        </div>
      </div>

      <div className="space-y-4">
        {filteredTemplates.length === 0 ? (
          <div className="text-center py-12">
            <BookOpen className="w-16 h-16 mx-auto text-muted-foreground mb-4" />
            <p className="text-muted-foreground">{t('no_templates_found')}</p>
          </div>
        ) : (
          filteredTemplates.map(template => (
            <div
              key={template.id}
              className="border rounded-lg overflow-hidden hover:border-primary/50 transition-colors"
            >
              <button
                onClick={() => handleTemplateClick(template)}
                className="w-full text-left p-4 bg-background hover:bg-muted/50 transition-colors"
              >
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <div className="flex items-center gap-2 mb-2">
                      <h3 className="font-semibold text-lg">{template.name}</h3>
                      <span className="px-2 py-1 text-xs rounded-full bg-primary/10 text-primary">
                        {template.type}
                      </span>
                    </div>

                    <div className="flex items-center gap-4 text-sm text-muted-foreground mb-2">
                      <span className="flex items-center gap-1">
                        <Star className="w-4 h-4" />
                        {template.usage_count}
                      </span>
                      <span className="px-2 py-1 bg-muted rounded">
                        {template.category}
                      </span>
                    </div>

                    <p className="text-sm text-foreground mb-3">
                      {template.description}
                    </p>

                    <div className="flex flex-wrap gap-2">
                      {template.tags.map(tag => (
                        <span
                          key={tag}
                          className="px-2 py-1 text-xs rounded bg-secondary/50 text-secondary-foreground"
                        >
                          {tag}
                        </span>
                      ))}
                    </div>
                  </div>

                  {expandedTemplate === template.id ? (
                    <ChevronUp className="w-5 h-5 text-muted-foreground flex-shrink-0" />
                  ) : (
                    <ChevronDown className="w-5 h-5 text-muted-foreground flex-shrink-0" />
                  )}
                </div>

                {expandedTemplate === template.id && (
                  <div className="mt-4 pt-4 border-t">
                    <div className="flex gap-3">
                      <button
                        onClick={() => onTemplateSelect && onTemplateSelect(template.id, template.name)}
                        className="flex-1 px-4 py-2 bg-primary text-primary-foreground rounded-lg hover:bg-primary/90 transition-colors"
                      >
                        {t('use_this_template')}
                      </button>
                      <button
                        onClick={() => handleUseTemplate(template)}
                        className="px-4 py-2 border rounded-lg hover:bg-muted transition-colors"
                      >
                        {t('preview')}
                      </button>
                    </div>
                  </div>
                )}
              </button>
            </div>
          ))
        )}
      </div>

      <div className="mt-8 text-center text-sm text-muted-foreground">
        <p>
          {t('showing')} {filteredTemplates.length} {t('of')} {templates.length} {t('templates')}
        </p>
      </div>
    </div>
  );
}
