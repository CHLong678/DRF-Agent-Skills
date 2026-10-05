# Scenario: Serializer-driven N+1

## Symptom

A list endpoint returns 100 rows and executes 201+ queries because a serializer accesses related customer/account data per object.

## Expected reasoning

1. Measure/query-count first.
2. Identify serializer relation access.
3. Choose `select_related()` for single-valued relations or `prefetch_related()` for collections.
4. Keep authorization scoping before optimization.
5. Verify query count and response semantics.

## Primary skill

`drf-orm-performance`

## Secondary skill

`drf-serializers`

## Bad fixes

- cache the endpoint without understanding the N+1
- add arbitrary DB indexes
- call `.select_related()` for reverse/many-to-many collections

## Verification

Add a realistic query-count regression test or equivalent instrumentation.
