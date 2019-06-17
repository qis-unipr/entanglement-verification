for i in {1..100}; do
sleep 1s &
python3 verifier.py 1 &
python3 prover.py 1;
done
