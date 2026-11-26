# Computational Systems Research

An independent research programme studying how computational systems can be modelled, observed, tested, and verified against explicit claims about their behaviour.

## Status

- Programme: exploratory
- Current study: not yet selected
- Novelty claim: none
- Repository purpose: research records, literature reviews, implementation audits, experimental protocols, results, and decisions

## Programme question

How can we establish whether a computational system satisfies a stated property under specified operating conditions, given incomplete observations and dependencies outside our control?

A test passing is not a universal guarantee. An internally consistent model is not proof that it represents a real deployment. When evidence is insufficient, the result must remain unknown.

## Current investigation

The initial idea of building a general black-box AI-agent regression framework has been set aside as a novelty claim. Existing work already covers behavioural regression, workflow boundary testing, execution assurance, authorization, fault injection, idempotency, recovery, and evidence integrity.

A possible next direction is independent reproduction and external-validity testing of published agent-execution assurance results. This remains provisional pending artifact inspection and review of distributed-systems prior art.

## Repository structure

- `research/`: programme, current question, and methods
- `literature/`: paper register and reviews
- `implementation-audits/`: source-level implementation audits
- `experiments/`: protocols, results, and reproduction records
- `data/`: data provenance and handling
- `decisions/`: dated research decisions

## Principles

1. Make claims narrow and falsifiable.
2. Separate author-reported results from independent reproduction.
3. Record negative findings and failed replications.
4. Pin versions, configurations, data, and commands.
5. State assumptions and observation limits.
6. Use an inconclusive outcome when evidence is insufficient.
7. Do not claim novelty until a documented prior-art review supports it.

No software license has been selected yet. Add an explicit license when intended outputs and reuse conditions are decided.
