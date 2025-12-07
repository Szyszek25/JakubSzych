"""
🔒 GUARDRAILS I BEZPIECZEŃSTWO - SZCZEGÓŁOWA IMPLEMENTACJA
System zabezpieczeń dla Asystenta AI dla Administracji
"""

from typing import Dict, List, Any, Tuple, Optional
from datetime import datetime
import re
import hashlib
import json

class SecurityGuardrails:
    """Zaawansowany system guardrails i bezpieczeństwa"""
    
    def __init__(self):
        # Limity
        self.max_document_size = 10 * 1024 * 1024  # 10MB
        self.max_query_length = 10000
        self.max_cases_per_user = 1000
        self.max_operations_per_hour = 100
        
        # Blokowane słowa kluczowe
        self.blocked_keywords = [
            "usuń", "usunąć", "kasuj", "delete", "drop",
            "truncate", "alter", "modify", "update system"
        ]
        
        # Wzorce danych osobowych
        self.personal_data_patterns = {
            "pesel": r"\b\d{11}\b",
            "nip": r"\b\d{3}-\d{3}-\d{2}-\d{2}|\d{3}-\d{2}-\d{2}-\d{3}\b",
            "regon": r"\b\d{9}|\d{14}\b",
            "konto_bankowe": r"\b\d{2}\s?\d{4}\s?\d{4}\s?\d{4}\s?\d{4}\s?\d{4}\s?\d{4}\b",
            "email": r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b",
            "telefon": r"\b\d{3}[\s-]?\d{3}[\s-]?\d{3}\b"
        }
        
        # Audit log
        self.audit_log: List[Dict] = []
        self.operation_counts: Dict[str, int] = {}
        self.last_reset = datetime.now()
        
        # Whitelist dozwolonych operacji
        self.allowed_operations = [
            "add_case", "analyze_case", "generate_decision",
            "check_deadlines", "get_case_summary"
        ]
    
    def validate_input(self, data: Any, data_type: str = "document") -> Tuple[bool, str]:
        """Zaawansowana walidacja danych wejściowych"""
        
        try:
            # Walidacja rozmiaru
            if data_type == "document":
                if isinstance(data, str) and len(data.encode('utf-8')) > self.max_document_size:
                    return False, f"Dokument przekracza limit {self.max_document_size / 1024 / 1024:.1f}MB"
                
                if isinstance(data, dict):
                    data_str = json.dumps(data)
                    if len(data_str.encode('utf-8')) > self.max_document_size:
                        return False, "Dokument przekracza limit rozmiaru"
            
            elif data_type == "query":
                if isinstance(data, str) and len(data) > self.max_query_length:
                    return False, f"Zapytanie przekracza limit {self.max_query_length} znaków"
            
            # Sprawdzenie niebezpiecznych słów kluczowych
            data_str = str(data).lower()
            for keyword in self.blocked_keywords:
                if keyword in data_str:
                    return False, f"Wykryto niebezpieczne słowo kluczowe: {keyword}"
            
            # Sprawdzenie SQL injection (podstawowe)
            sql_patterns = [
                r"(\b(SELECT|INSERT|UPDATE|DELETE|DROP|ALTER|CREATE|TRUNCATE)\b)",
                r"(--|;|\*|')",
                r"(\b(OR|AND)\s+\d+\s*=\s*\d+)"
            ]
            for pattern in sql_patterns:
                if re.search(pattern, data_str, re.IGNORECASE):
                    return False, "Wykryto potencjalną próbę SQL injection"
            
            # Sprawdzenie XSS (podstawowe)
            xss_patterns = [
                r"<script[^>]*>.*?</script>",
                r"javascript:",
                r"on\w+\s*="
            ]
            for pattern in xss_patterns:
                if re.search(pattern, data_str, re.IGNORECASE):
                    return False, "Wykryto potencjalną próbę XSS"
            
            return True, "OK"
            
        except Exception as e:
            return False, f"Błąd walidacji: {str(e)}"
    
    def sanitize_output(self, output: str) -> str:
        """Sanityzacja danych wyjściowych"""
        
        # Usuń tagi script
        output = re.sub(r"<script[^>]*>.*?</script>", "", output, flags=re.IGNORECASE | re.DOTALL)
        
        # Usuń javascript: links
        output = re.sub(r"javascript:", "", output, flags=re.IGNORECASE)
        
        # Usuń event handlers
        output = re.sub(r"on\w+\s*=\s*['\"][^'\"]*['\"]", "", output, flags=re.IGNORECASE)
        
        # Escape HTML (podstawowe)
        output = output.replace("<", "&lt;").replace(">", "&gt;")
        
        return output
    
    def detect_personal_data(self, text: str) -> Dict[str, List[str]]:
        """Wykrywanie danych osobowych w tekście"""
        detected = {}
        
        for data_type, pattern in self.personal_data_patterns.items():
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                detected[data_type] = matches
        
        return detected
    
    def anonymize_personal_data(self, text: str) -> Tuple[str, Dict[str, int]]:
        """Anonimizacja danych osobowych"""
        anonymized = text
        stats = {}
        
        for data_type, pattern in self.personal_data_patterns.items():
            matches = re.findall(pattern, anonymized, re.IGNORECASE)
            if matches:
                stats[data_type] = len(matches)
                # Zastąp hashem
                anonymized = re.sub(
                    pattern,
                    lambda m: f"[{data_type.upper()}_HASH_{hashlib.md5(m.group().encode()).hexdigest()[:8]}]",
                    anonymized,
                    flags=re.IGNORECASE
                )
        
        return anonymized, stats
    
    def check_rodo_compliance(self, data: Dict) -> Tuple[bool, List[str]]:
        """Sprawdzenie zgodności z RODO"""
        issues = []
        
        # Sprawdzenie czy dane osobowe są odpowiednio chronione
        data_str = json.dumps(data)
        personal_data = self.detect_personal_data(data_str)
        
        if personal_data:
            issues.append(f"Wykryto dane osobowe: {', '.join(personal_data.keys())}")
            issues.append("Wymagana anonimizacja przed przetwarzaniem")
        
        # Sprawdzenie czy są mechanizmy ochrony
        if "encryption" not in data.get("security_measures", []):
            issues.append("Brak informacji o szyfrowaniu danych")
        
        # Sprawdzenie czy jest podstawa prawna
        if "legal_basis" not in data:
            issues.append("Brak informacji o podstawie prawnej przetwarzania")
        
        return len(issues) == 0, issues
    
    def log_operation(self, operation: str, user: str, details: Dict):
        """Logowanie operacji dla audit trail"""
        
        # Sprawdzenie czy operacja jest dozwolona
        if operation not in self.allowed_operations:
            self.audit_log.append({
                "timestamp": datetime.now().isoformat(),
                "operation": operation,
                "user": user,
                "status": "BLOCKED",
                "reason": "Operation not in whitelist",
                "details": details
            })
            return False
        
        # Rate limiting
        if not self._check_rate_limit(user, operation):
            self.audit_log.append({
                "timestamp": datetime.now().isoformat(),
                "operation": operation,
                "user": user,
                "status": "RATE_LIMITED",
                "details": details
            })
            return False
        
        # Anonimizacja danych osobowych w logach
        sanitized_details = self._sanitize_log_details(details)
        
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "operation": operation,
            "user": self._hash_user_id(user),
            "status": "SUCCESS",
            "details": sanitized_details
        }
        
        self.audit_log.append(log_entry)
        
        # Ograniczenie rozmiaru logu
        if len(self.audit_log) > 10000:
            self.audit_log = self.audit_log[-10000:]
        
        return True
    
    def _check_rate_limit(self, user: str, operation: str) -> bool:
        """Sprawdzenie rate limiting"""
        # Reset liczników co godzinę
        if (datetime.now() - self.last_reset).seconds > 3600:
            self.operation_counts.clear()
            self.last_reset = datetime.now()
        
        key = f"{user}:{operation}"
        count = self.operation_counts.get(key, 0)
        
        if count >= self.max_operations_per_hour:
            return False
        
        self.operation_counts[key] = count + 1
        return True
    
    def _sanitize_log_details(self, details: Dict) -> Dict:
        """Sanityzacja szczegółów logu"""
        sanitized = {}
        details_str = json.dumps(details)
        
        # Anonimizacja danych osobowych
        anonymized, _ = self.anonymize_personal_data(details_str)
        
        try:
            sanitized = json.loads(anonymized)
        except:
            sanitized = {"sanitized": True, "original_length": len(details_str)}
        
        return sanitized
    
    def _hash_user_id(self, user_id: str) -> str:
        """Hashowanie ID użytkownika dla prywatności"""
        return hashlib.sha256(user_id.encode()).hexdigest()[:16]
    
    def get_audit_log(self, filters: Optional[Dict] = None) -> List[Dict]:
        """Pobranie logu audit z opcjonalnymi filtrami"""
        log = self.audit_log.copy()
        
        if filters:
            if "user" in filters:
                user_hash = self._hash_user_id(filters["user"])
                log = [entry for entry in log if entry.get("user") == user_hash]
            
            if "operation" in filters:
                log = [entry for entry in log if entry.get("operation") == filters["operation"]]
            
            if "status" in filters:
                log = [entry for entry in log if entry.get("status") == filters["status"]]
            
            if "date_from" in filters:
                log = [entry for entry in log if entry.get("timestamp") >= filters["date_from"]]
            
            if "date_to" in filters:
                log = [entry for entry in log if entry.get("timestamp") <= filters["date_to"]]
        
        return log
    
    def generate_security_report(self) -> Dict:
        """Generowanie raportu bezpieczeństwa"""
        now = datetime.now()
        last_24h = [entry for entry in self.audit_log 
                   if (now - datetime.fromisoformat(entry["timestamp"])).seconds < 86400]
        
        blocked = [entry for entry in last_24h if entry.get("status") == "BLOCKED"]
        rate_limited = [entry for entry in last_24h if entry.get("status") == "RATE_LIMITED"]
        
        return {
            "timestamp": now.isoformat(),
            "total_operations_24h": len(last_24h),
            "blocked_operations": len(blocked),
            "rate_limited_operations": len(rate_limited),
            "success_rate": (len(last_24h) - len(blocked) - len(rate_limited)) / max(len(last_24h), 1),
            "top_operations": self._get_top_operations(last_24h),
            "security_alerts": self._generate_security_alerts(last_24h)
        }
    
    def _get_top_operations(self, log: List[Dict]) -> List[Dict]:
        """Pobranie najczęstszych operacji"""
        operation_counts = {}
        for entry in log:
            op = entry.get("operation", "unknown")
            operation_counts[op] = operation_counts.get(op, 0) + 1
        
        return sorted(
            [{"operation": op, "count": count} for op, count in operation_counts.items()],
            key=lambda x: x["count"],
            reverse=True
        )[:10]
    
    def _generate_security_alerts(self, log: List[Dict]) -> List[Dict]:
        """Generowanie alertów bezpieczeństwa"""
        alerts = []
        
        # Alert: Zbyt wiele zablokowanych operacji
        blocked = [entry for entry in log if entry.get("status") == "BLOCKED"]
        if len(blocked) > 10:
            alerts.append({
                "level": "WARNING",
                "message": f"Wykryto {len(blocked)} zablokowanych operacji w ciągu 24h",
                "recommendation": "Sprawdź logi pod kątem prób ataków"
            })
        
        # Alert: Rate limiting
        rate_limited = [entry for entry in log if entry.get("status") == "RATE_LIMITED"]
        if len(rate_limited) > 50:
            alerts.append({
                "level": "INFO",
                "message": f"Wykryto {len(rate_limited)} operacji z rate limiting",
                "recommendation": "Rozważ zwiększenie limitów dla użytkowników"
            })
        
        return alerts

# ============================================================================
# PRZYKŁAD UŻYCIA
# ============================================================================

if __name__ == "__main__":
    guardrails = SecurityGuardrails()
    
    # Test walidacji
    test_data = "To jest testowy dokument administracyjny."
    is_valid, msg = guardrails.validate_input(test_data, "document")
    print(f"Walidacja: {is_valid}, {msg}")
    
    # Test wykrywania danych osobowych
    text_with_personal = "Jan Kowalski, PESEL: 12345678901, email: jan@example.com"
    detected = guardrails.detect_personal_data(text_with_personal)
    print(f"Wykryte dane osobowe: {detected}")
    
    # Test anonimizacji
    anonymized, stats = guardrails.anonymize_personal_data(text_with_personal)
    print(f"Zanonimizowany tekst: {anonymized}")
    print(f"Statystyki: {stats}")
    
    # Test logowania
    guardrails.log_operation("analyze_case", "user123", {"case_id": "SPR-001"})
    print(f"Log entries: {len(guardrails.audit_log)}")
    
    # Raport bezpieczeństwa
    report = guardrails.generate_security_report()
    print(f"\nRaport bezpieczeństwa:")
    print(json.dumps(report, indent=2, ensure_ascii=False))

