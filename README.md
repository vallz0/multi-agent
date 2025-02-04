# Multi-Agent System (MAS) with PADE

This project explores **Multi-Agent Systems (MAS)** using the **PADE framework** in Python. It simulates a marketplace where agents communicate using **FIPA-ACL messages**.

## Features
- **Seller Agent:** Responds to product requests.
- **Buyer Agent:** Requests product information from the seller.
- **FIPA-ACL Protocols:** Enables structured agent communication.
- **Timed Behavior:** Automates periodic requests.

## Installation
Ensure you have Python installed, then install PADE:

```bash
pip install pade
```

## Usage
Run the script by specifying a starting port:

```bash
python Agent1.py <start_port>
```
Example:
```bash
python Agent1.py 5000
```

## How It Works
1. The **Seller Agent** listens for requests.
2. The **Buyer Agent** sends a request for product information.
3. The seller replies with the available products.
4. Messages follow the **FIPA-ACL protocol**.

## Future Enhancements
- Implement negotiation protocols.
- Add more complex agent behaviors.
- Expand to multi-buyer and multi-seller interactions.
