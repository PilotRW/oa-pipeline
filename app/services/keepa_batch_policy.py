def effective_batch_limit(
    requested_limit: int,
    *,
    tokens_left: int,
    token_cost_per_item: int,
    configured_limit: int,
) -> int:
    if token_cost_per_item <= 0:
        return max(0, min(requested_limit, configured_limit))
    token_capacity = max(0, int(tokens_left)) // token_cost_per_item
    return max(
        0,
        min(requested_limit, max(1, configured_limit), token_capacity),
    )
