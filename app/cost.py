def calculate_cost_saved(prompt_tokens, completion_tokens, paid_input_price, paid_output_price):
    return (prompt_tokens * paid_input_price) + (completion_tokens * paid_output_price)


def categorize_quality_gap(free_score, paid_score):
    gap = paid_score - free_score

    if gap <= 5:
        return "negligible"
    elif gap <= 15:
        return "moderate"
    else:
        return "significant"
