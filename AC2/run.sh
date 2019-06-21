for i in {1..1000}; do
sleep 1s &
python3 verifier.py 16 &
python3 prover.py 16;
done
