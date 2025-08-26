"""
Few-shot examples and prompts for the FewShotClassifier.

This file contains carefully selected examples from the training data that represent
different classification scenarios: single labels, multiple labels, and complex cases.
"""

from typing import List, Dict, Any

# Fixed few-shot examples selected from the training data analysis
# These represent different scenarios: single labels, multiple labels, and edge cases
FEW_SHOT_EXAMPLES = [
    # Single label examples
    {
        'title': 'Hypertensive response during dobutamine stress echocardiography',
        'abstract': 'Among 3,129 dobutamine stress echocardiographic studies, a hypertensive response, defined as systolic blood pressure (BP) > or = 220 mm Hg and/or diastolic BP > or = 110 mm Hg, occurred in 30 patients (1%). Patients with this response more often had a history of hypertension and had higher resting systolic and diastolic BP before dobutamine infusion.',
        'label': 'Cardiovascular'
    },
    # Multiple label examples
    {
        'title': 'Adrenoleukodystrophy: survey of 303 cases: biochemistry, diagnosis, and therapy',
        'abstract': 'Adrenoleukodystrophy (ALD) is a genetically determined disorder associated with progressive central demyelination and adrenal cortical insufficiency. All affected persons show increased levels of saturated unbranched very-long-chain fatty acids, particularly hexacosanoate (C26:0), because of impaired capacity to degrade these acids. This degradation normally takes place in a subcellular organelle called the peroxisome, and ALD, together with Zellwegers cerebrohepatorenal syndrome, is now considered to belong to the newly formed category of peroxisomal disorders.',
        'label': 'Neurological|Hepatorenal'
    },
    {
        'title': 'The interpeduncular nucleus regulates nicotine effects on free-field activity',
        'abstract': 'Partial lesions were made with kainic acid in the interpeduncular nucleus of the ventral midbrain of the rat. Compared with sham-operated controls, lesions significantly (p < 0.25) blunted the early (<60 min) free-field locomotor hypoactivity caused by nicotine (0.5 mg kg(-1), i.m.), enhanced the later (60-120 min) nicotine-induced hyperactivity, and raised spontaneous nocturnal activity.',
        'label': 'Neurological'
    },
    {
        'title': 'Patterns of sulfadiazine acute nephrotoxicity',
        'abstract': 'Sulfadiazine acute nephrotoxicity is reviving specially because of its use in toxoplasmosis in HIV-positive patients. We report 4 cases, one of them in a previously healthy person. Under treatment with sulfadiazine they developed oliguria, abdominal pain, renal failure and showed multiple radiolucent renal calculi in echography.',
        'label': 'Hepatorenal'
    },
    {
        'title': 'Haplotype and phenotype analysis of six recurrent BRCA1 mutations in 61 families',
        'abstract': 'Several BRCA1 mutations have now been found to occur in geographically diverse breast and ovarian cancer families. To investigate mutation origin and mutation-specific phenotypes due to BRCA1, we constructed a haplotype of nine polymorphic markers within or immediately flanking the BRCA1 locus in a set of 61 breast/ovarian cancer families selected for having one of six recurrent BRCA1 mutations.',
        'label': 'Oncological'
    },
    
    {
        'title': 'corticosteroids and ventricular tachycardia: brain insights',
        'abstract': 'Purpose: This longitudinal study examined aspirin for hypertension in adult population. The investigation included analysis of breast cancer, gaba, and myelodysplastic syndrome. Methods: 345 participants were included. Results: reduction in adverse events. Implications: clinical practice guidelines.',
        'label': 'Neurological|Oncological'
    },
    {
        'title': 'tia and epilepsy: vascular insights',
        'abstract': 'Hypothesis: ACE inhibitors improves cancer outcomes via atrial fibrillation pathways. Methods: randomized controlled trial with 162 cancer patients, measuring hemodialysis and endothelial. Results: positive treatment response. Conclusion: clinical practice guidelines.',
        'label': 'Cardiovascular|Hepatorenal'
    },
    
    # Edge case with complex medical terminology
    {
        'title': 'Potential therapeutic use of the selective dopamine D1 receptor agonist, A-86929: an acute study in parkinsonian levodopa-primed monkeys',
        'abstract': 'The clinical utility of dopamine (DA) D1 receptor agonists in the treatment of Parkinson disease (PD) is still unclear. The therapeutic use of selective DA D1 receptor agonists such as SKF-82958 and A-77636 seems limited because of their duration of action, which is too short for SKF-82958 (< 1 hr) and too long for A-77636 (> 20 hr, leading to behavioral tolerance).',
        'label': 'Neurological'
    }
]

def get_few_shot_examples() -> List[Dict[str, Any]]:
    """
    Get the list of few-shot examples.
    
    Returns:
        List of example dictionaries with title, abstract, and label
    """
    return FEW_SHOT_EXAMPLES.copy()

def create_classification_prompt(text: str, labels: List[str], max_examples: int = 8) -> str:
    """
    Create a few-shot prompt for medical text classification.
    
    Args:
        text: Input text to classify (title + abstract)
        labels: List of available classification labels
        max_examples: Maximum number of few-shot examples to include
        
    Returns:
        Formatted prompt string for the Mistral model
    """
    prompt = "You are a medical text classifier. Classify the following medical article into one of these categories:\n"
    prompt += f"Categories: {', '.join(labels)}\n\n"
    
    # Add few-shot examples
    if FEW_SHOT_EXAMPLES:
        prompt += "Examples:\n"
        for example in FEW_SHOT_EXAMPLES[:max_examples]:
            prompt += f"Title: {example['title']}\n"
            prompt += f"Abstract: {example['abstract']}\n"
            prompt += f"Category: {example['label']}\n\n"
    
    # Add the text to classify
    prompt += "Classify the following article into one of these categories:\n"
    prompt += f"{text}\n"
    prompt += "Category:"
    
    return prompt

def get_prompt_info() -> Dict[str, Any]:
    """
    Get information about the prompts and examples.
    
    Returns:
        Dictionary with prompt information
    """
    return {
        'total_examples': len(FEW_SHOT_EXAMPLES),
        'example_labels': list(set(example['label'] for example in FEW_SHOT_EXAMPLES)),
        'single_label_count': len([ex for ex in FEW_SHOT_EXAMPLES if '|' not in ex['label']]),
        'multi_label_count': len([ex for ex in FEW_SHOT_EXAMPLES if '|' in ex['label']]),
        'description': 'Fixed examples with single labels, multiple labels, and complex medical terminology'
    }
