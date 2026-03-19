def calculate_metrics(predicted_entities, ground_truth_entities):
    """
    Calculates Precision, Recall, and F1-Score for entity extraction.
    """
    # Convert lists to sets for comparison
    pred_set = set(predicted_entities)
    true_set = set(ground_truth_entities)
    
    # True Positives: Entities correctly identified
    tp = len(pred_set.intersection(true_set))
    
    # False Positives: Entities identified by model but not in ground truth
    fp = len(pred_set - true_set)
    
    # False Negatives: Entities in ground truth but missed by model
    fn = len(true_set - pred_set)
    
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0
    f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
    
    return {
        "Precision": round(precision, 2),
        "Recall": round(recall, 2),
        "F1-Score": round(f1, 2)
    }

# Example Evaluation for 'SKILLS'
if __name__ == "__main__":
    ground_truth = ["Python", "Machine Learning", "SQL", "Deep Learning"]
    predictions = ["Python", "Machine Learning", "Java"] # Model missed SQL/DL, added Java incorrectly
    
    metrics = calculate_metrics(predictions, ground_truth)
    print(f"Evaluation Metrics: {metrics}")